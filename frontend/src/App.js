import "./App.css";
import Axios from 'axios';
import React,{useState,useEffect} from 'react';
function App() {
  const items = [
    {id: 1, name: 'draw up ( figma ) designs of what app looks like'},
    {id: 2, name: 'get api pulling'},
    {id: 3, name: 'get api displaying'},
    {id: 4, name: 'get api storing'},
    {id: 5, name: 'continue research on react etc'},
    {id: 6, name: 'begin research on machine learning / clustering / closest event first'}
  ];

  const[comments,setComments]=useState([])
  useEffect(() => {
    fetchComments();
  }, [])
  useEffect(() => {
    console.log(comments)
  }, [comments])

  const fetchComments = async() => {
    const response = await Axios('http://jsonplaceholder.typicode.com/comments');
    setComments(response.data)
  }

  return (
    <div className="App">
      <h1>Todo List</h1>

      <ul style={{alignItems:'left'}}>
        {items.map((item) => <li key={item.id}>{item.name}</li>)}
      </ul>

      <h2>Json Placeholder API - Comments</h2>
      {
        comments && comments.map(comment => {
          return(
            <div key={comment.id} style={{alignItems:'center',margin:'20px 60px'}}>
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
