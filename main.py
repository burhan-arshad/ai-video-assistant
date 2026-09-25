from dotenv import load_dotenv
load_dotenv()
from utils.video_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize_transcript, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from utils.video_processor import download_yt_video, convert_to_wav, audio_chunks
from core.rag_engine import build_rag_chain, ask_question

def run_pipeline(source:str, translate:bool=False):
    print("Starting pipeline...")
    chunks=process_input(source)
    print("Transcribing audio...")
    transcription=transcribe_all(chunks, translate)
    print("Transcription completed.")
    title=generate_title(transcription)
    summary=summarize_transcript(transcription)
    action_items=extract_action_items(transcription)
    key_decisions=extract_key_decisions(transcription)
    questions=extract_questions(transcription)
    rag_chain=build_rag_chain(transcription)
    return {
        "title": title,
        "transcription": transcription,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": key_decisions,
        "questions": questions,
        "rag_chain": rag_chain
    }

if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()

    translate = input("Translate audio to English? (y/n): ").strip().lower() == "y"
    if translate == 'y':
        translate = True

    result = run_pipeline(source, translate)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['questions']}")
    print("=" * 60)

    # Phase 2 — Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")

    rag_chain = result["rag_chain"]

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")