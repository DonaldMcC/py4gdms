/*npx cypress open - is the command to get started on these for now  */


describe('Signup users', function () {
  // we can use these values to log in
  const username = 'user1'
  const email = 'user1@user.com'
  const password = 'Testuser1'

  context('HTML form submission', function () {
    beforeEach(function () {
    })

    it('redirects to /index on success', function () {
      cy.visit('/auth/register')
      cy.get('#username').type(username)
      cy.get('#email').type(email)
      cy.get('#password').type(password)
      cy.get('#password2').type(password)
      cy.get('#firstname').type(username)
      cy.get('#lastname').type(username)
      cy.get('#submit').click()

      // we should be redirected to /dashboard
      cy.url().should('include', '/registered')
      cy.get('body').should('contain', 'Registered')

    })
  })

  })


