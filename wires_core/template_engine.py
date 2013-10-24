import re

class TemplateEngine:

    def __init__(self, template, definitions):
        self.template = template
        self.definitions = definitions

    def render(self):
        substitutions = {}
        for definition in self.definitions:
            substitutions[re.compile("<%=\s*{0}\s*%>".format(definition))] = self.definitions[definition]
        for substitution in substitutions:
            self.template = re.sub(substitution, substitutions[substitution], self.template)
        return self.template
