document.addEventListener('alpine:init', () => {
  Alpine.data('commentsManager', (logId, currentUserId) => ({
    logId: logId,
    currentUserId: currentUserId,
    comments: [],
    newComment: '',

    async init() {
      // Fetch the initial comments from your API endpoint.
      try {
        const res = await fetch(`/api/v2/habit_board/comments/`);
        this.comments = await res.json();
      } catch (error) {
        console.error("Failed to load comments", error);
      }
    },

    async postComment() {
      if (!this.newComment.trim()) return;
      const commentText = this.newComment.trim();
      try {
        // Post comment to your API
        const res = await fetch(`/api/logs/${this.logId}/comments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: commentText })
        });
        const postedComment = await res.json();
        // Add the new comment to the list
        this.comments.push(postedComment);
        this.newComment = '';
      } catch (error) {
        console.error("Error posting comment", error);
      }
    },

    async deleteComment(commentId) {
      try {
        const res = await fetch(`/api/comments/${commentId}`, {
          method: 'DELETE'
        });
        if (res.ok) {
          // Remove comment from the list
          this.comments = this.comments.filter(c => c.id !== commentId);
        }
      } catch (error) {
        console.error("Error deleting comment", error);
      }
    },

    async editComment(comment) {
      // For a simple inline edit, you could use a prompt.
      // Later, consider toggling an inline edit form.
      const newText = prompt("Edit your comment:", comment.text);
      if (!newText || newText.trim() === comment.text) return;
      try {
        const res = await fetch(`/api/comments/${comment.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: newText.trim() })
        });
        const updatedComment = await res.json();
        const index = this.comments.findIndex(c => c.id === comment.id);
        if (index !== -1) {
          this.comments.splice(index, 1, updatedComment);
        }
      } catch (error) {
        console.error("Error editing comment", error);
      }
    }
  }));
});
