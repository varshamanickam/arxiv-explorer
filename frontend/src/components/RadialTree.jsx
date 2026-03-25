function RadialTree({
    topCategories,
    subcategories,
    selectedTop,
    selectedSub,
    onTopClick,
    onSubClick,
  }) {
    const centerX = 520;
    const centerY = 360;
    const topRadius = 270;
    const subRadius = 150;
  
    const topNodes = topCategories.map((category, index) => {
      const angle = (2 * Math.PI * index) / topCategories.length - Math.PI / 2;
      const x = centerX + topRadius * Math.cos(angle);
      const y = centerY + topRadius * Math.sin(angle);
  
      return { category, x, y };
    });
  
    const selectedTopNode = topNodes.find((node) => node.category === selectedTop);
  
    const subNodes =
      selectedTop && selectedTopNode
        ? (subcategories[selectedTop] || []).map((sub, index, arr) => {
            const angle = (2 * Math.PI * index) / arr.length - Math.PI / 2;
            const x = selectedTopNode.x + subRadius * Math.cos(angle);
            const y = selectedTopNode.y + subRadius * Math.sin(angle);
  
            return { sub, x, y };
          })
        : [];
  
    return (
      <div className="radial-tree-container">
        <svg className="radial-tree-svg" viewBox="0 0 1040 720">
          {topNodes.map((node) => (
            <line
              key={`line-${node.category}`}
              x1={centerX}
              y1={centerY}
              x2={node.x}
              y2={node.y}
              className="tree-line"
            />
          ))}
  
          {selectedTopNode &&
            subNodes.map((node) => (
              <line
                key={`sub-line-${node.sub}`}
                x1={selectedTopNode.x}
                y1={selectedTopNode.y}
                x2={node.x}
                y2={node.y}
                className="tree-line sub-line"
              />
            ))}
  
          <g>
            <circle cx={centerX} cy={centerY} r="42" className="root-node" />
            <text x={centerX} y={centerY + 5} textAnchor="middle" className="node-label root-label">
              arXiv
            </text>
          </g>
  
          {topNodes.map((node) => (
            <g
              key={node.category}
              onClick={() => onTopClick(node.category)}
              className="clickable-node"
            >
              <circle
                cx={node.x}
                cy={node.y}
                r="30"
                className={
                  selectedTop === node.category ? "top-node active-node" : "top-node"
                }
              />
              <text
                x={node.x}
                y={node.y + 5}
                textAnchor="middle"
                className="node-label"
              >
                {node.category}
              </text>
            </g>
          ))}
  
          {subNodes.map((node) => (
            <g
              key={node.sub}
              onClick={() => onSubClick(node.sub)}
              className="clickable-node"
            >
              <circle
                cx={node.x}
                cy={node.y}
                r="22"
                className={
                  selectedSub === node.sub ? "sub-node active-sub-node" : "sub-node"
                }
              />
              <text
                x={node.x}
                y={node.y + 4}
                textAnchor="middle"
                className="sub-label"
              >
                {node.sub}
              </text>
            </g>
          ))}
        </svg>
      </div>
    );
  }
  
  export default RadialTree;

  