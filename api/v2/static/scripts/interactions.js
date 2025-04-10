async function postComment(userId, entityId, entityType, text) {
  const response = await fetch('/api/v2/comments', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, entity_id: entityId, entity_type: entityType, text: text })
  });
  return response.json();

}

async function fetchComments(entityId, entityType) {
  const response = await fetch(`/api/v2/comments/${entityId}/${entityType}`);
  const comments = await response.json();
  //console.log(comments);
}

async function removeComment(commentId) {
  const response = await fetch(`/api/v2/comments/${commentId}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ comment_id: commentId })
  });
  //console.log(response);
  return response;
}

async function addReaction(userId, entityId, entityType, reactionType) {
  const response = await fetch('/api/v2/reactions', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, entity_id: entityId, entity_type: entityType, reaction_type: reactionType })
  });

  const result = await response;
  //console.log(result);
  return result
}

async function fetchReactions(entityId, entityType) {
  const response = await fetch(`/api/v2/reactions/all/${entityId}/${entityType}`);
  const reactions = await response.json();
  //console.log(reactions);
}
async function fetchReactionsCount(entityId, entityType) {
  const response = await fetch(`/api/v2/reactions/counts/${entityId}/${entityType}`);
  const reactions = await response.json();
  //console.log(reactions);
}


async function removeReaction(userId, entityId, entityType) {
  const response = await fetch('/api/v2/reactions', {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, entity_id: entityId, entity_type: entityType })
  });

  const result = await response.json();
  //console.log(result);
}

