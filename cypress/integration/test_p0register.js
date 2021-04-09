/*npx cypress open - is the command to get started on these for now  */

describe('Signup users',  () => {
    // we can use these values to log in
    const operations = [
        {
            username: 'user1',
            email: 'user1@user.com',
            password: 'Testuser1'
        },
        {
            username: 'user2',
            email: 'user2@user.com',
            password: 'Testuser2'
        },
        {
            username: 'user3',
            email: 'user3@user.com',
            password: 'Testuser3'
        },
    ]

    // dynamically create a single test for each operation in the list
    operations.forEach((user) => {
        it('redirects to /index on success', function () {
            cy.visit('/auth/register')
            cy.get('#username').type(user.username)
            cy.get('#email').type(user.email)
            cy.get('#password').type(user.password)
            cy.get('#password2').type(user.password)
            cy.get('#firstname').type(user.username)
            cy.get('#lastname').type(user.username)
            cy.get('#submit').click()

            // we should be redirected to /dashboard
            cy.url().should('include', '/registered')
            cy.get('body').should('contain', 'Registered')

        })
    })
})



