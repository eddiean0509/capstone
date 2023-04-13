import FormError from "./formError";

export default function ReplyForm({ formRef, reply, errors, onClick }) {
  return (
    <div className="container">
      <h5 className="my-3 border-bottom pb-2">Modify the Reply</h5>
      <form ref={formRef}>
        {errors && <FormError errors={errors} />}
        <div className="mb-3">
          <label htmlFor="content">Content</label>
          <textarea
            className="form-control"
            name="content"
            rows="10"
            placeholder="(required)"
            defaultValue={reply && reply.content}
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary" onClick={onClick}>
          Save the Reply
        </button>
      </form>
    </div>
  );
}
