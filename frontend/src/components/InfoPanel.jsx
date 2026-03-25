import PaperCard from "./PaperCard";

function InfoPanel({ selectedTop, selectedSub, keyword, setKeyword, papers }) {
  const title = selectedTop
    ? selectedSub
      ? `${selectedTop}.${selectedSub}`
      : selectedTop
    : "No category selected";

  return (
    <div className="info-panel">
      <div className="panel-header">
        <h1>ArXiv Navigator</h1>
        <p className="panel-subtitle">Radial category map</p>
      </div>

      <div className="selection-block">
        <div className="label">Current Selection</div>
        <div className="selection-value">{title}</div>
      </div>

      <div className="selection-block">
        <div className="label">Keyword Filter</div>
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Search title or abstract..."
          className="search-input"
          disabled={!selectedTop}
        />
      </div>

      <div className="selection-block">
        <div className="label">Loaded Papers</div>
        <div className="selection-value">{papers.length}</div>
      </div>

      <div className="papers-list">
        {papers.length === 0 ? (
          <p className="empty-state">
            {selectedTop
              ? "No papers match the current filter."
              : "Select a category node to begin browsing."}
          </p>
        ) : (
          papers.slice(0, 100).map((paper, index) => (
            <PaperCard key={`${paper.id || paper.title}-${index}`} paper={paper} />
          ))
        )}
      </div>
    </div>
  );
}

export default InfoPanel;