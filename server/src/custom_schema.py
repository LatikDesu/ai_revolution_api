from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)

        excluded_endpoints = [
            'users/set_email/',
            'users/set_password/',
            'users/reset_email/',
            'users/reset_email_confirm/',
            'users/resend_activation/',

        ]

        paths = {}
        for path, path_data in swagger['paths'].items():
            include_path = True
            for endpoint in excluded_endpoints:
                if endpoint in path:
                    include_path = False
                    break

            if include_path:
                paths[path] = path_data

        swagger['paths'] = paths

        return swagger
