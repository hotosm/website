# Localization

## Translating Template Strings
Referenced from https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#internationalization-in-template-code
1. Add the `{% load i18n %}` tag to enable translation at the top of the template the strings are present in taking precedent over other load tags but taking place after extend template tags.
2. Wrap strings in a translate tag if it is a constant string or purely variable content as shown below.
	- `{% translate "Example string" %}`
	- `{% translate {{ title }} %}`
3. Wrap strings in a blocktrans tag if it is a mix of string literals and variable content.
	- `{% blocktranslate %}This string will have {{ value }} inside.{% endblocktranslate %}`
4. To generate the `.po` files for translation, run `make makemessages`
5. To compile the `.po` files into `.mo` to be able to present in in the application, run `make compilemessages`

## Guideline to Dividing Strings
The decision on how to divide the strings into translate tags depends on the context and the structure of the sentences. Here are some general guidelines:

1. **Whole sentences**: Whenever possible, translate whole sentences. This helps to preserve the context and makes the translations more accurate.

2. **Dynamic content**: If a sentence includes dynamic content (like variables), you can use the `{% blocktrans %}` tag to translate the whole sentence, including the dynamic content.

3. **HTML tags**: If a string includes HTML tags, you can include the tags in the `{% translate %}` or `{% blocktrans %}` tag. However, be aware that this can make the translations more difficult, as the translators will need to preserve the HTML tags in their translations.

4. **User interface elements**: Each distinct user interface element (like a button, a link, or a form field) should usually have its own `{% translate %}` tag.

In your provided code, each navigation link text is wrapped in a `{% translate %}` tag, which is a good practice. This allows each link text to be translated independently, which is important because the translation of a word or phrase can depend on its context.
