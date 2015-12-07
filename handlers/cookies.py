import webapp2

import main  # lol.. :/


class CookiesHandler(webapp2.RequestHandler):
  """ hand setting cookies and http response headers
  """
  def get(self):
    res = self.response

    res.set_cookie('browser', 'can read this one')
    res.set_cookie('nobrowser', 'this one is httponly', httponly=True)

    template = main.JINJA_ENVIRONMENT.get_template('templates/cookies.html')
    self.response.write(template.render())
