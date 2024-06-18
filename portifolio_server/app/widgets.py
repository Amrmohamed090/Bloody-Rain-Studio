from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe

class ResizableImageWidget(ClearableFileInput):
    template_name = 'widgets/resizable_image_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        html = self._render(self.template_name, context, renderer)
        return mark_safe(html)
    