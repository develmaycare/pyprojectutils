# Classes


class Issue(object):
    """A generic representation of a record from issue management."""

    def __init__(self, title, assigned_to=None, bucket=None, description=None, end_date=None, extra_columns=None,
                 labels=None, milestone=None, start_date=None, status=None):

        self.assigned_to = assigned_to
        self.bucket = bucket
        self.description = description
        self.end_date = end_date
        self.extra_columns = extra_columns or list()
        self.labels = labels or list()
        self.milestone = milestone
        self.start_date = start_date
        self.status = status or "Planning"
        self.title = title

    def get_tokens(self):
        """Get the issue as a list of values.

        :rtype: list
        :returns: Returns the properties in this order: title, description, start_date, end_date, bucket, status,
                  milestone, labels (CSV), assigned_to

        """
        return [
            self.title,
            self.description,
            self.start_date,
            self.end_date,
            self.bucket,
            self.status,
            self.milestone,
            ",".join(self.labels),
            self.assigned_to,
        ] + self.extra_columns

    def to_csv(self):
        """Get the issue as CSV.

        :rtype: str

        """
        tokens = self.get_tokens()

        # Convert the line into CSV. We can't use join because we need to wrap the tokens in quotes.
        line = ""
        for t in tokens:
            line += '"%s",' % t

        # Remove the last comma.
        line = line[:-1]

        # Return the line.
        return line

    def to_html(self):
        """Get the issue as HTML.

        :rtype: str

        """
        tokens = self.get_tokens()

        html = list()
        html.append("<tr>")

        for t in tokens:
            html.append("<td>%s</td>" % t)

        html.append("</tr>")

        return "\n".join(html)
