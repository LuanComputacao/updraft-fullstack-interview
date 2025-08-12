# Microinterações – AI Summary

Streaming

- Início: mostrar spinner no header e ARIA live (polite)
- Durante: typewriter a cada chunk; manter scroll ancorado na última linha
- Cancelar: botão Cancel — encerra a stream, preserva texto parcial e foca no editor
- Reconexão: tentativa única automática; se falhar, mostrar Retry

Botões e estados

- Generate (primary quando vazio)
- Save (primary quando há mudanças e não salvo)
- Regenerate, Delete, Copy (secondary)
- Disabled states durante streaming (exceto Cancel)

Feedback

- Toasts: Saved, Updated, Deleted, Error
- Timestamp da última geração
- Dica: "Edite livremente, depois clique em Save"
