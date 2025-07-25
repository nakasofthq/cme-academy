from django.db import models
from django.utils import timezone

from coupon.helpers import (
    get_random_code,
    get_coupon_code_length,
    get_user_model,
)


# Create your models here.
# ========================
class Ruleset(models.Model):
    allowed_users = models.ForeignKey(
        "AllowedUsersRule", on_delete=models.CASCADE, verbose_name="Valid Users"
    )
    max_uses = models.ForeignKey(
        "MaxUsesRule", on_delete=models.CASCADE, verbose_name="Max Usage Count"
    )
    validity = models.ForeignKey(
        "ValidityRule", on_delete=models.CASCADE, verbose_name="Coupon Expiration"
    )

    def __str__(self):
        return "Ruleset Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Coupon Validation"
        verbose_name_plural = "Coupon Validation"


class AllowedUsersRule(models.Model):
    user_model = get_user_model()

    users = models.ManyToManyField(user_model, verbose_name="Users", blank=True)
    all_users = models.BooleanField(default=False, verbose_name="All users?")

    def __str__(self):
        # return "AllowedUsersRule Nº{0}".format(self.id)
        return "ValidUsers Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Valid User"
        verbose_name_plural = "Valid Users"


class MaxUsesRule(models.Model):
    max_uses = models.BigIntegerField(default=0, verbose_name="Maximum Usage")
    is_infinite = models.BooleanField(default=False, verbose_name="Infinite Usage?")
    uses_per_user = models.IntegerField(default=1, verbose_name="Usage per user")

    def __str__(self):
        return "MaxUsesRule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Coupon Usage Condition"
        verbose_name_plural = "Coupon Usage Conditions"


class ValidityRule(models.Model):
    expiration_date = models.DateTimeField(verbose_name="Expiration date")
    is_active = models.BooleanField(default=False, verbose_name="Is active?")

    def __str__(self):
        return "ValidityRule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Coupon Exipiration"
        verbose_name_plural = "Coupon Exipirations"


class CouponUser(models.Model):
    user_model = get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name="User")
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.CASCADE, verbose_name="Coupon"
    )
    times_used = models.IntegerField(
        default=0, editable=False, verbose_name="Usage Count"
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Coupon User"
        verbose_name_plural = "Coupon Users"


class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Value")
    is_percentage = models.BooleanField(default=False, verbose_name="Is percentage?")

    def __str__(self):
        if self.is_percentage:
            return "{0}%".format(self.value)
            # return "{0}% - Discount".format(self.value)

        return "₦{0}".format(self.value)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"


class Coupon(models.Model):
    code_length = get_coupon_code_length()

    code = models.CharField(
        max_length=code_length,
        default=get_random_code,
        verbose_name="Coupon Code",
        unique=True,
    )
    discount = models.ForeignKey("Discount", on_delete=models.CASCADE)
    times_used = models.IntegerField(
        default=0, editable=False, verbose_name="Usage Count"
    )
    created = models.DateTimeField(editable=False, verbose_name="Coupon Creation date")

    ruleset = models.ForeignKey(
        "Ruleset", on_delete=models.CASCADE, verbose_name="Coupon Validation"
    )

    def __str__(self):
        return self.code

    def use_coupon(self, user):
        coupon_user, created = CouponUser.objects.get_or_create(user=user, coupon=self)
        coupon_user.times_used += 1
        coupon_user.save()

        self.times_used += 1
        self.save()

    def get_discount(self):
        return {
            "value": self.discount.value,
            "is_percentage": self.discount.is_percentage,
        }

    def get_discounted_value(self, initial_value):
        discount = self.get_discount()

        if discount["is_percentage"]:
            new_price = initial_value - ((initial_value * discount["value"]) / 100)
            new_price = new_price if new_price >= 0.0 else 0.0
        else:
            new_price = initial_value - discount["value"]
            new_price = new_price if new_price >= 0.0 else 0.0

        return new_price

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Coupon, self).save(*args, **kwargs)
