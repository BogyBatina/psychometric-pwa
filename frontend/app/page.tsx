"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    console.log("Backend URL:", backendUrl); // Debugging

    fetch(`${backendUrl}/api/tests`)
      .then((response) => response.json())
      .then((data) => setTests(data))
      .catch((error) => console.error("Error fetching tests:", error));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Available Tests</h1>
      <ul>
        {tests.map((test: { id: number; title: string }) => (
          <li key={test.id}>{test.title}</li>
        ))}
      </ul>
    </div>
  );
}
