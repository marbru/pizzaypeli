1.This is a django app. As part of the "showtimes" app I want to create a page where people can vote for future movies to show at a cinema. I want to list the proposed movies along with a vote count. I want to allow people to add a new movie (just the title), and vote for any of the proposed movies.
  ![1](claude_log/1.png)


2. I now want to also track the movies that have been shown.

  Let's add a "showed_at" date field to the model. From the voting page, we should have a way to mark a movie as shown, with a datepicker to select the date.

  Shown movies should not appear on the voting list. We show add a new page titled "previously shown", listing the previous movies from more recent to least recent. The voting page should be renamed "upcoming".

  Since we now have two pages, "upcoming" and "previously shown", we should add a header to the page with navigation links to access them.

  ![2](claude_log/2.png)

  3. Can we extract the css on a static file? 

  4. UI is currently very bloated. I'd like to remove the date picker and show it as a hover when you click "mark as shown". And when you pick the date, then the form is submitted

    ![4](claude_log/4.png)