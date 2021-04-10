/*npx cypress open - is the command to get started on these for now  */

describe('Signup users',  () => {
    // we can use these values to log ind
    const username = 'user2'
    const password = 'Testuser2'


    const operations = [
        {
            url: '/new_question/0/action',
            text: 'Lets get this done'
        },
        {
            url: '/new_question/0/action',
            text: 'The world is under-achieving'
        },
        {
            url: '/new_question/0/action',
            text: 'Need actions working'
        },
    ]

    // dynamically create a single test for each operation in the list
    operations.forEach((action) => {

                it('can visit /users', function () {
                    // or another protected page
                    cy.visit('/auth/login?next=../index')
                    cy.get('#signin').type(username)
                    cy.get('#signpass').type(password)
                    cy.get('#login').click()

                    cy.visit(action.url)
                    cy.get('#question_questiontext').type(action.text)

                   cy.get('input[type=submit]').click()

                    cy.url().should('include', '/questiongrid')
                    cy.get('body').should('contain', action.text)
                })
    })
})



