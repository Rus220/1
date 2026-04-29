import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Pains from "@/components/Pains";
import Process from "@/components/Process";
import Cases from "@/components/Cases";
import Trust from "@/components/Trust";
import Fears from "@/components/Fears";
import LeadForm from "@/components/LeadForm";
import About from "@/components/About";
import FinalCTA from "@/components/FinalCTA";
import Footer from "@/components/Footer";
import StickyButtons from "@/components/StickyButtons";

export default function Home() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Pains />
        <Process />
        <Cases />
        <Trust />
        <Fears />
        <LeadForm />
        <About />
        <FinalCTA />
      </main>
      <Footer />
      <StickyButtons />
    </>
  );
}
