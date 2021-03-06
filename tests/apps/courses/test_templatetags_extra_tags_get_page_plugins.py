"""Test suite for the GetPagePlugins template tag."""
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.template.exceptions import TemplateSyntaxError
from django.test import RequestFactory

from classytags.exceptions import ArgumentRequiredError
from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase

from richie.plugins.simple_text_ckeditor.cms_plugins import CKEditorPlugin


class GetPagePluginsTemplateTagsTestCase(CMSTestCase):
    """
    Integration tests to validate the behavior of the `get_page_plugins` template tag.
    """

    @transaction.atomic
    def test_templatetags_get_page_plugins_missing_page_lookup(self):
        """
        The "get_page_plugins" template tag should fail if the page_lookup arg is missing.
        """
        page = create_page("Test", "richie/single_column.html", "en", published=True)
        placeholder = page.placeholders.all()[0]
        add_plugin(placeholder, CKEditorPlugin, "en", body="<b>Test</b>")

        request = RequestFactory().get("/")
        request.current_page = page
        request.user = AnonymousUser()

        template = (
            "{% load cms_tags extra_tags %}"
            '{% get_page_plugins "maincontent" as plugins %}'
        )
        with self.assertRaises(ArgumentRequiredError) as context:
            self.render_template_obj(template, {}, request)
        self.assertEqual(context.exception.argname, "page_lookup")
        self.assertEqual(context.exception.tagname, "get_page_plugins")

    @transaction.atomic
    def test_templatetags_get_page_plugins_with_page_lookup(self):
        """
        The "get_page_plugins" template tag should inject in the context, the plugins
        of the targeted placeholder on the page targeted by a page lookup.
        """
        page = create_page("Test", "richie/single_column.html", "en", published=True)
        placeholder = page.placeholders.all()[0]
        add_plugin(placeholder, CKEditorPlugin, "en", body="<b>Test 1</b>")
        add_plugin(placeholder, CKEditorPlugin, "en", body="<b>Test 2</b>")

        request = RequestFactory().get("/")
        request.current_page = create_page(
            "current", "richie/single_column.html", "en", published=True
        )
        request.user = AnonymousUser()

        template = (
            "{% load cms_tags extra_tags %}"
            '{% get_page_plugins "maincontent" page as plugins %}'
            "{% for plugin in plugins %}{% render_plugin plugin %}{% endfor %}"
        )
        output = self.render_template_obj(template, {"page": page}, request)
        self.assertEqual(output, "<b>Test 1</b>\n<b>Test 2</b>\n")

    @transaction.atomic
    def test_templatetags_get_page_plugins_empty(self):
        """
        The "get_page_plugins" template tag should render its node content if it has
        no plugins and the "or keyword is passed.
        """
        empty_page = create_page(
            "Test", "richie/single_column.html", "en", published=True
        )
        page = create_page("Test", "richie/single_column.html", "en", published=True)
        placeholder = page.placeholders.all()[0]
        add_plugin(placeholder, CKEditorPlugin, "en", body="<b>Test</b>")

        request = RequestFactory().get("/")
        request.current_page = create_page(
            "current", "richie/single_column.html", "en", published=True
        )
        request.user = AnonymousUser()

        template = (
            "{% load cms_tags extra_tags %}"
            '{% get_page_plugins "maincontent" page as plugins or %}'
            "<i>empty content</i>{% endget_page_plugins %}"
            "{% for plugin in plugins %}{% render_plugin plugin %}{% endfor %}"
        )
        output = self.render_template_obj(template, {"page": page}, request)
        self.assertEqual("<b>Test</b>\n", output)

        output = self.render_template_obj(template, {"page": empty_page}, request)
        self.assertEqual("<i>empty content</i>", output)

    @transaction.atomic
    def test_templatetags_get_page_plugins_empty_no_or(self):
        """
        The "get_page_plugins" template tag should raise an error if it has block
        content but the "or keyword was forgotten.
        """
        empty_page = create_page(
            "Test", "richie/single_column.html", "en", published=True
        )

        request = RequestFactory().get("/")
        request.current_page = create_page(
            "current", "richie/single_column.html", "en", published=True
        )
        request.user = AnonymousUser()

        template_without_or = (
            "{% load cms_tags extra_tags %}"
            '{% get_page_plugins "maincontent" page as plugins %}'
            "<i>empty content</i>{% endget_page_plugins %}"
        )

        with self.assertRaises(TemplateSyntaxError):
            self.render_template_obj(template_without_or, {"page": empty_page}, request)

    @transaction.atomic
    def test_templatetags_get_page_plugins_unknown_placeholder(self):
        """
        When a new placeholder is added to the code, it does not exist on pages that were
        pre-existing. The `get_page_plugins` should not fail in this case.
        """
        page = create_page("Test", "richie/single_column.html", "en", published=True)

        request = RequestFactory().get("/")
        request.current_page = page
        request.user = AnonymousUser()

        template = (
            "{% load cms_tags extra_tags %}"
            '{% get_page_plugins "unknown" page as plugins %}'
            "{% for plugin in plugins %}{% render_plugin plugin %}{% endfor %}"
        )
        output = self.render_template_obj(template, {"page": page}, request)
        self.assertEqual(output, "")

    def test_templatetags_get_page_plugins_unknown_page(self):
        """
        The `get_page_plugins` template tag should fail nicely when called with a page
        lookup that returns no page.
        """
        request = RequestFactory().get("/")
        request.current_page = create_page(
            "current", "richie/single_column.html", "en", published=True
        )
        request.user = AnonymousUser()

        template = (
            "{% load cms_tags extra_tags %}"
            '{% get_page_plugins "maincontent" page as plugins %}'
        )

        output = self.render_template_obj(template, {"page": "unknown"}, request)
        self.assertEqual(output, "")
