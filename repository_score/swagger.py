from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    schema = coreapi.Document(
        title='Popular Github Repositories',
        url='/',
        content={
            'check_repository_is_popular': coreapi.Link(
                url='/api/check_repository_is_popular',
                action='get',
                fields=[
                    coreapi.Field(
                        name='repository_name',
                        required=True,
                        location='query',
                        description='Repository name to check if is popular.',
                        type="string",
                    )
                ],
                description='Returns if a repository is popular or not based on the internal score.',
            ),
            'health_status': coreapi.Link(
                url='/api/health_status',
                action='get',
                description='Returns the health status of the system.'
            )
        }
    )
    return response.Response(schema)
