function App() {
  const items = [
    {id: 1, name: 'draw up ( figma ) designs of what app looks like'},
    {id: 2, name: 'get api pulling'},
    {id: 3, name: 'get api displaying'},
    {id: 4, name: 'get api storing'},
    {id: 5, name: 'continue research on react etc'},
    {id: 6, name: 'begin research on machine learning / clustering / closest event first'}
  ];

  return (
    <>
      <h1>Todo List</h1>
      <ul>
        {items.map((item) => <li key={item.id}>{item.name}</li>)}
      </ul>
    </>
  );
}

// TODO : continue research
// TODO : use/check api methods and dataframe accessing in richweb GithubAPI problem

export default App;
