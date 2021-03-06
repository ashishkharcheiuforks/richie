describe('Course run view', function() {
  beforeEach(() => {
    // Start from the courses list view (we know its URL)
    cy.visit('/en/courses/');
    // Find the first open course (eg. with the enroll CTA) and open it
    cy.contains('Enroll now').click();
    // Find the first open course run (there is one since the course had the Enroll CTA) and open it
    cy.contains('See details').click();
    cy.injectAxe();
  });

  it('passes axe a11y checks', () => {
    cy.checkA11y();
  });
});
