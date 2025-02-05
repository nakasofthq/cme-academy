from django.http import Http404
from functools import wraps






GENDER_CHOICES = (
    ('', '---'),
    ('M', 'Male'),
    ('F', 'Female'),
)


CATEGORY_CHOICES = (
    ('plan', 'Plan'),
    ('affiliate', 'Affiliate'),
)


PLAN_CHOICES = (
    ('free', 'Free'),
    ('basic', 'Basic'),
    ('advance', 'Advance'),
    ('pro', 'Pro'),
)


AFFILIATE_CHOICES = (
    ('free', 'Free'),
    ('gold', 'Gold'),
)


DURATION_CHOICES = (
    ('1', '1 Month'),
    ('2', '2 Months'),
    ('3', '3 Months'),
    ('4', '4 Months'),
    ('5', '5 Months'),
    ('6', '6 Months'),
    ('7', '7 Months'),
    ('8', '8 Months'),
    ('9', '9 Months'),
    ('10', '10 Months'),
    ('11', '11 Months'),
    ('12', '12 Months'),
    # ('13', '13 Months'),
    # ('14', '14 Months'),
    # ('15', '15 Months'),
    # ('16', '16 Months'),
    # ('17', '17 Months'),
    # ('18', '18 Months'),
    # ('19', '19 Months'),
    # ('20', '20 Months'),
    # ('21', '21 Month'),
    # ('22', '22 Months'),
    # ('23', '23 Months'),
    # ('24', '24 Months'),
)


# DURATION_CHOICES = (
#     (1, '1 Month'),
#     (2, '2 Months'),
#     (3, '3 Months'),
#     (4, '4 Months'),
#     (5, '5 Months'),
#     (6, '6 Months'),
#     (7, '7 Months'),
#     (8, '8 Months'),
#     (9, '9 Months'),
#     (10, '10 Months'),
#     (11, '11 Months'),
#     (12, '12 Months'),
#     # (13, '13 Months'),
#     # (14, '14 Months'),
#     # (15, '15 Months'),
#     # (16, '16 Months'),
#     # (17, '17 Months'),
#     # (18, '18 Months'),
#     # (19, '19 Months'),
#     # (20, '20 Months'),
#     # (21, '21 Month'),
#     # (22, '22 Months'),
#     # (23, '23 Months'),
#     # (24, '24 Months'),
# )


FEE_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
)


COUNTRY_CHOICES = (
    ('NGA', 'Nigeria'),
)


STATE_CODE_CHOICES = (
    ('', '---'),
	('AB', 'Abia'),
    ('FC', 'Abuja (FCT)'),
	('AD', 'Adamawa'),
	('AN', 'Anambra'),
	('AK', 'Akwa Ibom'),
	('BA', 'Bauchi'),
	('BY', 'Bayelsa'),
	('BN', 'Benue'),
	('BR', 'Borno'),
	('CR', 'Cross River'),
	('DE', 'Delta'),
	('EB', 'Ebonyi'),
	('ED', 'Edo'),
	('EK', 'Ekiti'),
	('EN', 'Enugu'),
	('GM', 'Gombe'),
	('IM', 'Imo'),
	('JG', 'Jigawa'),
	('KD', 'Kaduna'),
	('KN', 'Kano'),
	('KT', 'Katsina'),
	('KB', 'Kebbi'),
	('KG', 'Kogi'),
	('KW', 'Kwara'),
	('LA', 'Lagos'),
	('NW', 'Nasarawa'),
	('NG', 'Niger'),
	('OG', 'Ogun'),
	('ON', 'Ondo'),
	('OS', 'Osun'),
	('OY', 'Oyo'),
	('PL', 'Plateau'),
	('RV', 'Rivers'),
	('SO', 'Sokoto'),
	('TR', 'Taraba'),
	('YB', 'Yobe'),
	('ZF', 'Zamfara'),
)


STATE_NAME_CHOICES = (
    ('', '---'),
    ('Abia', 'Abia'),
	('Abuja', 'Abuja (FCT)'),
    ('FCT', 'FCT(Abuja)'),
    ('Adamawa', 'Adamawa'),
    ('Anambra', 'Anambra'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
)


# STATUS = (
#     (0, 'Start'),
#     (1, 'Stop'),
# )






def ajax_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax:
            raise Http404
        return function(request, *args, **kwargs)
    return wrap

