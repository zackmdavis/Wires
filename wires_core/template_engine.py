import re

class TemplateEngine:

    def __init__(self, template, definitions):
        self.master = open('./views/layouts/application.html').read()
        self.template = template
        self.definitions = definitions
        self.substitutions = {}
        for definition in self.definitions:
            self.substitutions[re.compile("<%=\s*{0}\s*%>".format(definition))] = self.definitions[definition]

    def render_partial(self):
        page = self.template
        for substitution in self.substitutions:
            page = re.sub(substitution, self.substitutions[substitution], page)
        return page

    def render(self):
        page = self.render_partial()
        page = re.sub("<%=\s*yield\s*%>", page, self.master)
        for substitution in self.substitutions:
            page = re.sub(substitution, self.substitutions[substitution], page)
        return page
