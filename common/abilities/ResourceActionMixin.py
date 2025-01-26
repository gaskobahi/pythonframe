class ResourceActionMixin:
    resource_action_map = {}  # Define in subclasses

    def get_resource_action(self):
        return self.resource_action_map.get(self.request.method, None)

    def get_resource_subject(self):
        return self.__class__.__name__.replace("View", "")  # e.g., 'CategoryListCreate'
