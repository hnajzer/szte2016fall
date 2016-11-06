Feature: Series database handling
  An API for adding, removing and updating a series

  Scenario: Initially there are no series
    Given the database is empty
    When I request all series
    Then I receive a 200 status code response
    And there are 0 series

  Scenario: Create a new series with missing data
    Given the database is empty
    When I create a series called "Black mirror"
    Then I receive a 400 status code response

  Scenario: Create a new series
    Given the database is empty
    When I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    Then I receive a 200 status code response
    And there are 1 series

  Scenario: Create a new series
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    And I create a series called "Halt and catch fire" with summary "I am the product!" and with 3 seasons
    When I get this series back
    Then there are 2 series
    And the series title is "Halt and catch fire"
    And the series summary is "I am the product!"
    And the series has 3 seasons

  Scenario: Can get a series
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    When I get this series back
    Then the series title is "Black mirror"
    And the series summary is "It's a good series"
    And the series has 2 seasons

  Scenario: Can delete a series
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    When I delete this series
    Then I receive a 200 status code response

  Scenario: Can not delete a series twice
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    When I delete this series
    And I delete this series
    Then I receive a 404 status code response

  Scenario: Can not get deleted series
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    When I delete this series
    And I get this series back
    Then I receive a 404 status code response

  Scenario: Can modify series
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    When I modify the summary to "It's a bad series"
    Then I receive a 200 status code response

  Scenario: Can modify series
    Given the database is empty
    And I create a series called "Black mirror" with summary "It's a good series" and with 2 seasons
    When I modify the summary to "It's a bad series"
    And I get this series back
    Then the series title is "Black mirror"
    And the series summary is "It's a bad series"
    And the series has 2 seasons