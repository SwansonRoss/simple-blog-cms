from wtforms import Form, StringField, validators, TextAreaField, widgets, PasswordField

class BlogForm(Form):
        title = StringField(u'Post Title', [validators.required()])
        subhead = StringField(u'Subhead', [validators.optional()])
        preview = TextAreaField(u'Preview', [validators.optional()])
        image = StringField(u'Image URL', [validators.optional()])
        copy = TextAreaField(u'Post Copy', [validators.required()])

class LoginForm(Form):
    username = StringField(u'User Name', [validators.required()])
    password = PasswordField(u'Password', [validators.required()])

class SetPasswordForm(Form):
    username = StringField(u'Enter username', [validators.email()])
    password = PasswordField(u'Enter Password', [validators.required()])
    passwordVerify = PasswordField(u'Re-enter Password', [validators.required()])

class SiteInfoForm(Form):
    title = StringField(u'Blog Site Title', [validators.required()])
    tagLine = StringField(u'Tagline', [validators.optional()])
    author = StringField(u'Author Name', [validators.optional()])
    about = TextAreaField(u'About this blog', [validators.optional()])
    authorImage = StringField(u'Author Image URL', [validators.optional()])
    