export default function SearchBar({ searchTerm, setSearchTerm }) {    
    return (
        <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="searchBar"
        />
    );
}