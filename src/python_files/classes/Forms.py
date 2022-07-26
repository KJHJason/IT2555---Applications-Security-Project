# import third party libraries
from wtforms import Form, validators, StringField, TextAreaField, EmailField, IntegerField, PasswordField, SelectField

# import local python libraries
from .Constants import CONSTANTS

class CreateLoginForm(Form):
    email = EmailField("Email:", [validators.Email(), validators.Length(min=5, max=254), validators.DataRequired()])
    password = PasswordField("Password:", [validators.DataRequired()])

class CreateSignUpForm(Form):
    username = StringField("Username:", [validators.Length(min=1, max=30), validators.DataRequired()])
    email = EmailField("Email:", [validators.Email(), validators.Length(min=5, max=254), validators.DataRequired()])
    password = PasswordField(
        "Password:", [
            validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH),
            validators.DataRequired()
        ]
    )
    cfmPassword = PasswordField(
        "Confirm Password:", [
            validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH), 
            validators.DataRequired()
        ]
    )

class CreateChangeUsername(Form):
    updateUsername = StringField("Enter a new username:", [validators.Length(min=1, max=30), validators.DataRequired()])

class CreateChangeEmail(Form):
    updateEmail = EmailField("Enter a new email address:", [validators.Email(), validators.Length(min=3, max=254), validators.DataRequired()])
    currentPassword = PasswordField("Enter your current password:", [validators.Length(min=6, max=20), validators.DataRequired()])

class CreateChangePasswordForm(Form):
    currentPassword = PasswordField(
        "Enter your current password:", [
            validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH),
            validators.DataRequired()
        ]
    )
    password =  PasswordField(
        "Enter a new password:", [
            validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH), 
            validators.DataRequired()
        ]
    )
    cfmPassword = PasswordField("Confirm password:", [validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH), validators.DataRequired()])

class RecoverAccountMFAForm(Form):
    email = EmailField("Enter your email address:", [validators.Email(), validators.Length(min=3, max=254), validators.DataRequired()])
    backupCode = StringField("Enter your backup code:", [validators.Length(min=19, max=19), validators.DataRequired()])

class RequestResetPasswordForm(Form):
    email = EmailField("Enter your email:", [validators.Email(), validators.Length(min=3, max=254), validators.DataRequired()])

class CreateResetPasswordForm(Form):
    password =  PasswordField("Reset password:", [
            validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH),
            validators.DataRequired()
        ]
    )
    cfmPassword = PasswordField("Confirm password:", [
            validators.Length(min=CONSTANTS.MIN_PASSWORD_LENGTH, max=CONSTANTS.MAX_PASSWORD_LENGTH), 
            validators.DataRequired()
        ]
    )

class AdminRecoverForm(Form):
    email = EmailField("Enter user's new email:", [validators.Email(), validators.Length(min=3, max=254), validators.DataRequired()])

class twoFAForm(Form):
    twoFATOTP = StringField("Enter the 6 Digit Code:", [validators.Length(min=6, max=6), validators.DataRequired()])

class CreateCourse(Form):
    courseTitle = StringField("Course Title: ", [validators.DataRequired(), validators.Length(min=3, max=100)])
    courseDescription = TextAreaField("Description: ", [validators.DataRequired(), validators.Length(min=1, max=5000)])
    coursePrice = IntegerField("Price for Course (USD$): ", [validators.DataRequired(), validators.NumberRange(min=0, max=500)])

class CreateCourseEdit(Form):
    courseTitle = StringField("Course Title: ", [validators.Length(min=3, max=100)])
    courseDescription = TextAreaField("Description: ", [validators.Length(min=1, max=5000)])
    coursePrice = IntegerField("Price for Course (USD$): ", [validators.NumberRange(min=0, max=500)])

class CreateReview(Form):
    reviewDescription = TextAreaField("Description: ", [validators.DataRequired(), validators.Length(min=1, max=5000)])
    reviewTitle = TextAreaField("Title: ", [validators.DataRequired(), validators.Length(min=1, max=100)])

class UpdateRoles(Form):
    roleName = StringField("Role Name: ", [validators.DataRequired(), validators.Length(min=3, max=100)])
    guestBP = SelectField("Guest BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    generalBP = SelectField("General BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    adminBP = SelectField("Admin BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    loggedInBP = SelectField("Logged In BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    errorBP=SelectField("Error BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    teacherBP = SelectField("Teacher BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    userBP = SelectField("Student BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])
    superAdminBP = SelectField("Super Admin BP: ", [validators.DataRequired()], choices=[('1', 'Enable'), ('0', 'Disable')])

class CreateAdmin(Form):
    username=StringField("Enter username:", [validators.Length(min=1, max=30), validators.DataRequired()])
    email = EmailField("Enter user's new email:", [validators.Email(), validators.Length(min=3, max=254), validators.DataRequired()])