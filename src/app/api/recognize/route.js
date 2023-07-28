import { NextResponse } from "next/server";

export async function POST(request, { params }) {
  const requestJSON = await request.json();

  const response = await fetch(`${process.env.API_ENDPOINT}/recognize`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestJSON),
  });

  const responseJSON = await response.json();

  return NextResponse.json(responseJSON);
}
