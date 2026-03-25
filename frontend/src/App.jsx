import { useMemo, useState } from "react";
import "./App.css";
import InfoPanel from "./components/InfoPanel";
import RadialTree from "./components/RadialTree";
import treeData from "./data/frontend_tree_data.json";

function App() {
  const [selectedTop, setSelectedTop] = useState(null);
  const [selectedSub, setSelectedSub] = useState(null);
  const [keyword, setKeyword] = useState("");

  const topCategories = treeData.top_categories;
  const subcategories = treeData.subcategories;
  const papersByCategory = treeData.papers_by_category;
  const papersLookup = treeData.papers;

  const currentKey = selectedTop
    ? selectedSub
      ? `${selectedTop}.${selectedSub}`
      : selectedTop
    : null;

  const currentPapers = useMemo(() => {
    if (!currentKey) return [];

    const paperIds = papersByCategory[currentKey] || [];
    const papers = paperIds
      .map((id) => papersLookup[id])
      .filter(Boolean);

    const lowered = keyword.trim().toLowerCase();

    if (!lowered) return papers;

    return papers.filter((paper) => {
      const title = (paper.title || "").toLowerCase();
      const abstract = (paper.abstract || "").toLowerCase();
      return title.includes(lowered) || abstract.includes(lowered);
    });
  }, [currentKey, keyword, papersByCategory, papersLookup]);

  const handleTopClick = (top) => {
    setSelectedTop(top);
    setSelectedSub(null);
    setKeyword("");
  };

  const handleSubClick = (sub) => {
    setSelectedSub(sub);
    setKeyword("");
  };

  return (
    <div className="app-shell">
      <div className="tree-panel">
        <RadialTree
          topCategories={topCategories}
          subcategories={subcategories}
          selectedTop={selectedTop}
          selectedSub={selectedSub}
          onTopClick={handleTopClick}
          onSubClick={handleSubClick}
        />
      </div>

      <div className="info-panel-wrapper">
        <InfoPanel
          selectedTop={selectedTop}
          selectedSub={selectedSub}
          keyword={keyword}
          setKeyword={setKeyword}
          papers={currentPapers}
        />
      </div>
    </div>
  );
}

export default App;