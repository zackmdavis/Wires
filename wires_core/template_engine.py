import re

class TemplateEngine:

    def __init__(self, template, definitions):
        self.master = open('./views/layouts/application.html').read()
        self.template = template
        self.definitions = definitions

    def render(self):
        substitutions = {}
        for definition in self.definitions:
            substitutions[re.compile("<%=\s*{0}\s*%>".format(definition))] = self.definitions[definition]
        page = self.template
        for substitution in substitutions:
            page = re.sub(substitution, substitutions[substitution], page)
        page = re.sub("<%=\s*yield\s*%>", page, self.master)
        return page
