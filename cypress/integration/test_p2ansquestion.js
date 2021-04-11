/*npx cypress open - is the command to get started on these for now  */

describe('Answer Actions',  () => {
    // we can use these values to log ind
    const username = 'user2'
    const password = 'Testuser2'


    const operations = [
        {
            url: '/index/questions',
            answer: 'Approve'
        },
        {
            url: '/index/questions',
            answer: 'Approve'
        },
        {
            url: '/index/questions',
            answer: 'Approve'
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
                   cy.get("td:nth-child(2) > .is-success").click()
                    cy.get('body').should('contain', 'Answer recorded')
                })
    })
})


