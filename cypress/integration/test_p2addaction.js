/*npx cypress open - is the command to get started on these for now  */

describe('Signup users',  () => {
    // we can use these values to log ind
    const username = 'user2'
    const password = 'Testuser2'


    const operations = [
        {
            url: '/new_question/0/action',
            action: 'Lets get this done'
        },
        {
            url: '/new_question/0/action',
            action: 'The world is under-achieving'
        },
        {
            url: '/new_question/0/action',
            action: 'Need actions working'
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

        })
    })
})



