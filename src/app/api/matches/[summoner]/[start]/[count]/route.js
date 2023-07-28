import { NextResponse } from "next/server";

export async function GET(request, { params }) {
  const response = await fetch(
    `${process.env.API_ENDPOINT}/matches/${params.summoner}/${params.start}/${params.count}`
  );
  const responseJSON = await response.json();

  return NextResponse.json(responseJSON);
}
