Feature: Movie database handling
  An API for adding, removing and updating a movie database

  Scenario: Request a non existing movie by id
    Given The app is running
    And I have no movies in the database
    When I request the movie with ID 1
    Then I receive a 404 status code response

  Scenario: Request an existing movie by id
    Given The app is running
    And I have a movie called "Interstellar", 2014 directed by "Christopher Nolan" under ID 1
    When I request the movie with ID 1
    Then I receive a 200 status code response

  Scenario: Delete a non existing movie by id
    Given The app is running
    And I have no movies in the database
    When I delete the movie with ID 1
    Then I receive a 404 status code response

  Scenario: Delete existing movie by id
    Given The app is running
    And I have a movie called "Interstellar", 2014 directed by "Christopher Nolan" under ID 1
    When I delete the movie with ID 1
    Then I receive a 200 status code response

  Scenario: Create non existing movie
    Given The app is running
    And I have no movies in the database
    And I create a movie called "Planet of the Apes", 1968 directed by "Franklin J. Schaffner"
    Then I receive a 200 status code response

  Scenario: Create movie duplicate movie
    Given The app is running
    And I have no movies in the database
    And I create a movie called "Interstellar", 2014 directed by "Christopher Nolan"
    And I create a movie called "Interstellar", 2014 directed by "Christopher Nolan"
    Then I receive a 409 status code response

  Scenario: Update non existing movie
    Given The app is running
    And I have no movies in the database
    And I update the movie under ID 1 with a movie called "Interstellar", 2014 directed by "Christopher Nolan"
    Then I receive a 404 status code response

  Scenario: Update existing movie
    Given The app is running
    And I have no movies in the database
    And I create a movie called "Interstellarrr", 2014 directed by "Christopher Nolan"
    And I update the movie under ID 1 with a movie called "Interstellar", 2014 directed by "Christopher Nolan"
    When I request the movie with ID 1
    Then I receive a 200 status code response