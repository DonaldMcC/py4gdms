/*npx cypress open - is the command to get started on these for now  */


describe('Logging In - HTML Web Form', function () {
    // we can use these values to log in
    const username = 'user1'
    const email = 'user1@user.com'
    const password = 'Testuser1'


        it('can visit /users', function () {
            // or another protected page
            cy.visit('/auth/login?next=../index')
            cy.get('#signin').type(username)
            cy.get('#signpass').type(password)
            cy.get('#login').click()

            cy.url().should('include', '/index')
            cy.get('body').should('contain', 'Project')

            cy.visit('/datasetup')
            cy.get('body').should('contain', 'successfully')

        })


})



