# payments/management/commands/generate_swagger_spec.py

from drf_yasg.generators import SchemaGenerator
from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):
    help = 'Generates Swagger specification and saves it to swagger.json'

    def handle(self, *args, **options):
        # Initialize the schema generator
        generator = SchemaGenerator()
        
        # Generate the schema
        schema = generator.get_schema(request=None, public=True)
        
        # Save the schema to a file
        with open('swagger.json', 'w') as f:
            json.dump(schema, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS('Swagger specification saved to swagger.json'))
