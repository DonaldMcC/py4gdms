/*npx cypress open - is the command to get started on these for now  */

describe('Signup users',  () => {
    // we can use these values to log ind
    const username = 'user2'
    const password = 'Testuser2'


    const operations = [
        {
            url: '/new_question/0/question',
            text: 'To be or not to be',
            ans1: 'be',
            ans2: 'not to be',
            resmethod: 'Standard'
        },
        {
            url: '/new_question/0/action',
            text: 'Will questions work',
            ans1: 'yes',
            ans2: 'no',
            resmethod: 'Single'
        },
        {
            url: '/new_question/0/issue',
            text: 'Will questions work',
            ans1: 'yes',
            ans2: 'no',
            resmethod: 'Single'
        }
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



