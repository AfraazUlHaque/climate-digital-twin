import { useEffect, useState } from "react";
import { getRegions } from "../api/api";

export default function RegionSelector({ region, setRegion }) {
  const [regions, setRegions] = useState(["Kerala", "Tamil Nadu"]);

  useEffect(() => {
    async function load() {
      try {
        const list = await getRegions();
        if (list.length) setRegions(list);
      } catch {
        setRegions(["Kerala", "Tamil Nadu"]);
      }
    }

    load();
  }, []);

  return (
    <select className="select" value={region} onChange={(e) => setRegion(e.target.value)}>
      {regions.map((r) => (
        <option key={r} value={r}>
          {r}
        </option>
      ))}
    </select>
  );
}