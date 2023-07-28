import "./globals.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import Footer from "@/components/layout/Footer";

export const metadata = {
  title: "LOLRECS",
  description: "LOL Recommendation",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta property="og:image" content="https://www.lolrecs.com/meta.png" />
      </head>
      <body>
        {children}
        <Footer />
      </body>
    </html>
  );
}
