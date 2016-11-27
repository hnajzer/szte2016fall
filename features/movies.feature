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

  Scenario: Request an existing movie by id
    Given The app is running
    And I have a movie called "Frankenweenie", 2012 directed by "Tim Burton" under ID 2
    When I request the movie with ID 2
    Then I receive a 200 status code response

  Scenario: Request an existing movie by id
    Given The app is running
    And I have a movie called "Donnie Darko", 2001 directed by "Richard Kelly" under ID 3
    When I request the movie with ID 3
    Then I receive a 200 status code response

  Scenario: Request an existing movie by id
    Given The app is running
    And I have a movie called "Planet of the Apes", 2001 directed by "Tim Burton" under ID 4
    When I request the movie with ID 4
    Then I receive a 200 status code response

  Scenario: Request an existing movie by id
    Given The app is running
    And I have a movie called "Planet of the Apes", 1968 directed by "Franklin J. Schaffner" under ID 5
    When I request the movie with ID 5
    Then I receive a 200 status code response
