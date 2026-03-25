function PaperCard({ paper }) {
    const abstractPreview = paper.abstract
      ? paper.abstract.slice(0, 180) + (paper.abstract.length > 180 ? "..." : "")
      : "No abstract available.";
  
    return (
      <div className="paper-card">
        <h3 className="paper-title">{paper.title || "Untitled Paper"}</h3>
  
        {paper.authors && <p className="paper-authors">{paper.authors}</p>}
  
        <p className="paper-abstract">{abstractPreview}</p>
  
        <div className="paper-tags">
          {(paper.categories || []).map((cat, index) => {
            const label = cat.subtopic
              ? `${cat.top_level}.${cat.subtopic}`
              : cat.top_level;
  
            return (
              <span key={`${label}-${index}`} className="paper-tag">
                {label}
              </span>
            );
          })}
        </div>
      </div>
    );
  }
  
  export default PaperCard;