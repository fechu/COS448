from django.contrib import admin


class CommonAdmin(admin.ModelAdmin):
    """
    Attributes:
        show_add_action:    Should the default add action be shown.
    """

    show_add_button = True

    def changelist_view(self, request, extra_context=None):
        response = super(CommonAdmin, self).changelist_view(request, extra_context)

        # Add button actions to the context data
        response.context_data['button_actions'] = self.get_button_actions()
        response.context_data['show_add_button'] = self.show_add_button

        return response

    def get_button_actions(self):
        """
        These buttons are added on the top right.
        Returns: A list of tuples containing a title and a url where the button should point to.
        """
        return []


