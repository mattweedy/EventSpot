import "./App.css";
import Axios from 'axios';
import React, { useState, useEffect } from 'react';
function App() {
  const items = [
    { id: 1, name: 'draw up ( figma ) designs of what app looks like' },
    { id: 2, name: 'continue research on react etc' },
    { id: 3, name: 'begin research on machine learning / clustering / closest event first' },
    { id: 4, name: 'create landing page - this week 2' },
    { id: 5, name: 'create base recommender [use sample data / generate sample data via mongodb] - week 3 & 4' },
  ];

  const week2 = [
    { id: 1, name: 'quiz questions' },
    { id: 2, name: 'diagrams of database design', detail: {
                                                            first: 'users',
                                                            second: 'events',
                                                            third: 'other?'
                                                          } },
    { id: 3, name: 'wireframes of webapp', detail: {
                                                    first: 'landing page',
                                                    second: 'quiz page',
                                                    third: 'login/signup',
                                                    fourth: 'events/rec page'
                                                  } },
    { id: 4, name: 'use case diagrams', detail: { first: 'refer to wireframes for idea' } }
  ]

  const laterItems = [
    { id: 1, name: 'get api pulling' },
    { id: 2, name: 'get api displaying' },
    { id: 3, name: 'get api storing' },
  ]

  const [comments, setComments] = useState([])

  useEffect(() => {
    fetchComments();
  }, [])
  useEffect(() => {
    console.log(comments)
  }, [comments])

  const fetchComments = async () => {
    const response = await Axios('http://jsonplaceholder.typicode.com/comments');
    setComments(response.data)
  }

  return (
    <div className="App">
      <h1>Todo List</h1>
      <ul>
        {items.map((item) => <li key={item.id}>{item.name}</li>)}
      </ul>

      <h2>Week 2</h2>
      <ul>
        {week2.map((item) => <li key={item.id}>{item.name}</li>)}
      </ul>

      <h2>Week 3/4</h2>
      <ul>
        {laterItems.map((item) => <li key={item.id}>{item.name}</li>)}
      </ul>


      <h2>Json Placeholder API - Comments</h2>
      {
        // check comments exists before displaying each (sliced to display first 15)
        comments && comments.slice(0, 15).map(comment => {
          return (
            <div key={comment.id} style={{ alignItems: 'center', margin: '20px 60px' }}>
              <h4>{comment.name}</h4>
              <p>{comment.body}</p>
              <p>{comment.email}</p>
            </div>
          )
        })
      }
    </div>
  );
}

// TODO : continue research
// TODO : use/check api methods and dataframe accessing in richweb GithubAPI problem

export default App;
