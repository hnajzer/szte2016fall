Feature: Movie database handling
  An API for adding, removing and updating a movie database

  Scenario: Request a non existing movie by id
    Given The app is running
    And I have no movies in the database
    When I request the movie with ID 1
    Then I receive a 404 status code response

  Scenario: Request an existing movie by id
    Given The app is running
    And I have a movie called "Interstellar" (2014) directed by "Christopher Nolan" under ID 1
    When I request the movie with ID 1
    Then I receive a 200 status code response
