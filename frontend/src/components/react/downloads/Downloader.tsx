import { useState, type FormEvent, type ChangeEvent } from "react";

export default function Downloader() {
  const [url, setUrl] = useState<string>("");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [message, setMessage] = useState<string>("");

  const handleDownload = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Validación corregida para enlaces reales de Spotify
    if (!url.includes("spotify.com")) {
      setStatus("error");
      setMessage("Por favor, introduce un enlace válido de Spotify.");
      return;
    }

    setStatus("loading");
    setMessage(
      "Magia en proceso: Leyendo Spotify y descargando en el servidor. Esto puede tardar unos minutos...",
    );

    try {
      const response = await fetch("http://localhost:8000/descargar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = "playlist_descargada.zip";
        document.body.appendChild(link);
        link.click();
        link.remove();

        setStatus("success");
        setMessage(`¡Éxito! Tu música se ha descargado.`);
      } else {
        const errorData = await response.json();
        setStatus("error");
        setMessage(errorData.detail || "Ocurrió un error al descargar.");
      }
    } catch (error) {
      setStatus("error");
      setMessage(
        "Error de conexión con el servidor. ¿Está encendido el backend?",
      );
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
  };

  return (
    <div className="w-full max-w-2xl mt-8 mx-auto text-left z-20 relative">
      <form onSubmit={handleDownload} className="relative group">
        <div className="absolute -inset-1 bg-primary/20 rounded-xl blur opacity-25 group-focus-within:opacity-100 transition duration-1000 group-focus-within:duration-200"></div>
        <div className="relative flex flex-col sm:flex-row items-stretch gap-2 bg-white dark:bg-slate-800/50 p-2 rounded-xl border border-slate-200 dark:border-slate-700 backdrop-blur shadow-2xl">
          <div className="flex flex-1 items-center px-4 gap-3">
            <span className="material-symbols-outlined text-slate-400">
              link
            </span>
            <input
              type="url"
              placeholder="Paste Spotify track or playlist URL here..."
              value={url}
              onChange={handleInputChange}
              className="w-full bg-transparent border-none outline-none focus:ring-0 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 text-lg py-3"
              required
            />
          </div>
          <button
            type="submit"
            disabled={status === "loading"}
            className="bg-primary text-background-dark px-8 py-4 rounded-lg text-lg font-bold hover:brightness-110 transition-all flex items-center justify-center gap-2 min-w-[160px] disabled:opacity-75 disabled:cursor-not-allowed"
          >
            <span
              className={`material-symbols-outlined ${status === "loading" ? "animate-spin" : ""}`}
            >
              {status === "loading" ? "sync" : "download"}
            </span>
            {status === "loading" ? "Processing" : "Download"}
          </button>
        </div>
      </form>

      {message && (
        <div
          className={`mt-6 p-4 rounded-lg font-medium text-center border ${
            status === "error"
              ? "bg-red-500/10 text-red-400 border-red-500/20"
              : status === "loading"
                ? "bg-blue-500/10 text-blue-400 border-blue-500/20"
                : "bg-primary/10 text-primary border-primary/20"
          }`}
        >
          {message}
        </div>
      )}

      <p className="mt-4 text-slate-500 dark:text-slate-500 text-sm text-center">
        Supports Tracks, Playlists, and Albums. Over 2M songs converted daily.
      </p>
    </div>
  );
}
