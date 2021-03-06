import re

class TemplateEngine:

    def __init__(self, template, definitions):
        self.master = open('./templates/layouts/application.html').read()
        self.template = template
        self.definitions = definitions.copy()
        for definition in self.definitions:
            self.definitions[definition] = str(self.definitions[definition])
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
        page = self.ignore_unused_prompts(page)
        return page

    @staticmethod
    def ignore_unused_prompts(page):
        return re.sub("<%=\s*\S+\s*%>", "", page)
