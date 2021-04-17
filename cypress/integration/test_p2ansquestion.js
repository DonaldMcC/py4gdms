/*npx cypress open - is the command to get started on these for now  */

describe('Answer Actions',  () => {
    // we can use these values to log ind

    const operations = [
        {
            user: 'user1',
            password: 'Testuser1',
            url: '/index/actions',
            answer: 'Approve',
            result: 'Answer recorded'
        },
        {
            user: 'user2',
            password: 'Testuser2',
            url: '/index/actions',
            answer: 'Approve',
            result: 'in progress'
        },
        {
            user: 'user3',
            password: 'Testuser3',
            url: '/index/actions',
            answer: 'Approve',
            result: 'Resolved'
        }
    ]

    // dynamically create a single test for each operation in the list
    operations.forEach((action) => {

                it('can visit /users', function () {
                    // or another protected page
                    cy.visit('/auth/login?next=../index')
                    cy.get('#signin').type(action.user)
                    cy.get('#signpass').type(action.password)
                    cy.get('#login').click()

                    cy.visit(action.url)
                   cy.get("td:nth-child(2) > .is-success").first().click()
                    cy.get('body').should('contain', action.result)
                })
    })
})
