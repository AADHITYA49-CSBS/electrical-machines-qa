from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

try:
    import markdown as _markdown
except Exception:
    _markdown = None

try:
    import bleach as _bleach
except Exception:
    _bleach = None


def _sanitize_html(html):
    if not _bleach:
        # Basic removal of script tags if bleach not installed
        import re
        html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.S | re.I)
        return html

    allowed_tags = [
        'p', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'code', 'pre', 'br', 'hr'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'rel'],
    }
    return _bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)


@register.filter(is_safe=False)
def markdown_to_html(value):
    """Convert markdown text to sanitized HTML. Falls back safely if markdown/bleach missing."""
    if not value:
        return ''

    if _markdown:
        html = _markdown.markdown(value, extensions=['extra', 'sane_lists'])
    else:
        # Fallback: escape and preserve line breaks
        return mark_safe('<div class="answer-content">%s</div>' % escape(value).replace('\n', '<br>'))

    safe_html = _sanitize_html(html)
    return mark_safe(safe_html)
