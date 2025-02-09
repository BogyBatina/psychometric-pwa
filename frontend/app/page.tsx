"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/tests")
      .then((response) => response.json())
      .then((data) => setTests(data));
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
