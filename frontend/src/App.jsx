import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // --------------------------------------------------
  // SELECT EXCEL FILE
  // --------------------------------------------------

  const selectExcelFile = async () => {
    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/select-file`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to select file."
        );
      }

      setFile(data);

    } catch (error) {
      alert(error.message);

    } finally {
      setLoading(false);
    }
  };


  // --------------------------------------------------
  // NEW CHAT
  // --------------------------------------------------

  const handleNewChat = () => {
    setMessages([]);
    setFile(null);
    setMessage("");
  };


  // --------------------------------------------------
  // SEND MESSAGE
  // --------------------------------------------------

  const handleSend = async () => {

    if (!message.trim()) {
      return;
    }

    if (!file) {
      alert(
        "Please attach an Excel file first."
      );

      return;
    }

    const userMessage = message.trim();

    // Show user's message immediately

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {

      const response = await fetch(
        `${API_URL}/execute`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            file_id: file.file_id,
            prompt: userMessage,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Excel operation failed."
        );
      }

      // ------------------------------------------------
      // SUCCESS RESPONSE
      // ------------------------------------------------

      setMessages((previous) => [
        ...previous,

        {
          role: "assistant",
          type: "success",
          data: data,
        },

      ]);

    } catch (error) {

      setMessages((previous) => [
        ...previous,

        {
          role: "assistant",
          type: "error",
          text: error.message,
        },

      ]);

    } finally {
      setLoading(false);
    }
  };


  // --------------------------------------------------
  // GET FILE NAME
  // --------------------------------------------------

  const getFileName = (path) => {

    if (!path) {
      return "";
    }

    return path
      .split("\\")
      .pop();
  };


  // --------------------------------------------------
  // RENDER READ RESULT
  // --------------------------------------------------

  const renderReadResult = (data) => {

    const result = data.result;

    // ----------------------------------------------
    // SINGLE VALUE
    // ----------------------------------------------

    if (
      result &&
      Object.prototype.hasOwnProperty.call(
        result,
        "value"
      )
    ) {

      return (
        <div className="read-result-card">

          <div className="read-result-header">

            <div className="success-icon">
              ✓
            </div>

            <div>

              <strong>
                Excel information found
              </strong>

              <span>
                No changes were made to the file.
              </span>

            </div>

          </div>


          <div className="read-result-body">

            <label>
              {result.field || "VALUE"}
            </label>

            <div className="read-value">
              {String(result.value)}
            </div>

          </div>


          <div className="read-result-footer">

            <span>
              File
            </span>

            <strong>
              {getFileName(data.file)}
            </strong>

            <span>
              Sheet
            </span>

            <strong>
              {data.sheet}
            </strong>

          </div>

        </div>
      );
    }


    // ----------------------------------------------
    // LIST OF VALUES
    // ----------------------------------------------

    if (
      result &&
      Array.isArray(result.values)
    ) {

      return (
        <div className="read-result-card">

          <div className="read-result-header">

            <div className="success-icon">
              ✓
            </div>

            <div>

              <strong>
                Excel information found
              </strong>

              <span>
                No changes were made to the file.
              </span>

            </div>

          </div>


          <div className="read-list-body">

            <label>
              {result.field || "VALUES"}
            </label>

            <div className="read-list">

              {result.values.map(
                (value, index) => (

                  <div
                    className="read-list-item"
                    key={index}
                  >

                    <span>
                      {index + 1}
                    </span>

                    <strong>
                      {String(value)}
                    </strong>

                  </div>

                )
              )}

            </div>

          </div>


          <div className="read-result-footer">

            <span>
              File
            </span>

            <strong>
              {getFileName(data.file)}
            </strong>

            <span>
              Total
            </span>

            <strong>
              {result.values.length}
            </strong>

          </div>

        </div>
      );
    }


    // ----------------------------------------------
    // ENTIRE ROW / OBJECT
    // ----------------------------------------------

    if (
      result &&
      typeof result === "object"
    ) {

      return (
        <div className="read-result-card">

          <div className="read-result-header">

            <div className="success-icon">
              ✓
            </div>

            <div>

              <strong>
                Excel information found
              </strong>

              <span>
                No changes were made to the file.
              </span>

            </div>

          </div>


          <div className="read-object-body">

            {Object.entries(result).map(
              ([key, value]) => (

                <div
                  className="read-object-row"
                  key={key}
                >

                  <span>
                    {key}
                  </span>

                  <strong>
                    {String(value)}
                  </strong>

                </div>

              )
            )}

          </div>


          <div className="read-result-footer">

            <span>
              File
            </span>

            <strong>
              {getFileName(data.file)}
            </strong>

            <span>
              Sheet
            </span>

            <strong>
              {data.sheet}
            </strong>

          </div>

        </div>
      );

    }


    return (
      <div className="error-card">

        <div className="error-icon">
          !
        </div>

        <div>

          <strong>
            No information found
          </strong>

          <p>
            The Excel file did not contain
            a result for this request.
          </p>

        </div>

      </div>
    );

  };


  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (

    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            ✦
          </div>

          <div>

            <div className="brand-name">
              AI Excel Automation
            </div>

            <div className="brand-subtitle">
              Automation Agent
            </div>

          </div>

        </div>


        <button
          className="new-chat-button"
          onClick={handleNewChat}
        >

          <span>
            ＋
          </span>

          New Chat

        </button>


        <div className="sidebar-bottom">

          <div className="agent-status">

            <span className="status-dot"></span>

            <div>

              <div className="status-title">
                Local Agent
              </div>

              <div className="status-text">
                Connected
              </div>

            </div>

          </div>

        </div>

      </aside>


      {/* MAIN */}

      <main className="main">


        {/* TOP BAR */}

        <header className="topbar">

          <div>

            <h1>
              AI Excel Automation
            </h1>

            <p>
              Modify your Excel files using natural language.
            </p>

          </div>


          <div className="connection">

            <span className="status-dot"></span>

            Local Agent Connected

          </div>

        </header>


        {/* CHAT AREA */}

        <section className="chat-area">


          {/* WELCOME */}

          {!messages.length && (

            <div className="welcome">

              <div className="welcome-icon">
                ✦
              </div>

              <h2>
                AI Excel Automation
              </h2>

              <p>
                Attach an Excel file and describe what
                you want to change using natural language.
              </p>

            </div>

          )}


          {/* MESSAGES */}

          <div className="messages">


            {messages.map(
              (item, index) => (

                <div
                  key={index}
                  className={`message-row ${item.role}`}
                >


                  {/* AI AVATAR */}

                  {item.role === "assistant" && (

                    <div className="avatar ai-avatar">
                      ✦
                    </div>

                  )}


                  <div className="message-content">


                    {/* USER MESSAGE */}

                    {item.role === "user" && (

                      <>

                        <div className="message-label">
                          You
                        </div>

                        <div className="user-bubble">
                          {item.text}
                        </div>

                      </>

                    )}


                    {/* AI SUCCESS */}

                    {item.role === "assistant" &&
                      item.type === "success" && (

                      <>

                        <div className="message-label">
                          AI Excel Automation
                        </div>


                        {/* READ RESULT */}

                        {(item.data.operation === "find" ||
                          item.data.operation === "read") && (

                          renderReadResult(
                            item.data
                          )

                        )}


                        {/* MODIFICATION RESULT */}

                        {item.data.operation !== "find" &&
                          item.data.operation !== "read" && (

                          <div className="result-card">


                            <div className="result-header">

                              <div className="success-icon">
                                ✓
                              </div>

                              <div>

                                <strong>
                                  Excel updated successfully
                                </strong>

                                <span>
                                  Your file was modified in place.
                                </span>

                              </div>

                            </div>


                            <div className="result-grid">


                              <div>

                                <label>
                                  FILE
                                </label>

                                <strong>
                                  {getFileName(
                                    item.data.file
                                  )}
                                </strong>

                              </div>


                              <div>

                                <label>
                                  SHEET
                                </label>

                                <strong>
                                  {item.data.sheet}
                                </strong>

                              </div>


                              <div>

                                <label>
                                  {item.data.operation === "add_row"
                                    ? "ROW"
                                    : "CELL"}
                                </label>

                                <strong>
                                  {item.data.operation === "add_row"
                                    ? item.data.row
                                    : item.data.cell}
                                </strong>

                              </div>


                              <div>

                                <label>
                                  VERIFICATION
                                </label>

                                <strong className="verified">
                                  ✓ {item.data.verification}
                                </strong>

                              </div>


                            </div>


                            {/* ADD ROW RESULT */}

                            {item.data.operation === "add_row" && (

                              <div className="read-object-body">

                                <label>
                                  ADDED VALUES
                                </label>

                                {item.data.values &&
                                  Object.entries(
                                    item.data.values
                                  ).map(
                                    ([key, value]) => (

                                      <div
                                        className="read-object-row"
                                        key={key}
                                      >

                                        <span>
                                          {key}
                                        </span>

                                        <strong>
                                          {String(value)}
                                        </strong>

                                      </div>

                                    )
                                  )}

                              </div>

                            )}


                            {/* NORMAL CELL MODIFICATION RESULT */}

                            {item.data.operation !== "add_row" && (

                              <div className="change-row">


                                <div>

                                  <label>
                                    OLD VALUE
                                  </label>

                                  <div className="value-box old">
                                    {String(
                                      item.data.old_value
                                    )}
                                  </div>

                                </div>


                                <div className="arrow">
                                  →
                                </div>


                                <div>

                                  <label>
                                    NEW VALUE
                                  </label>

                                  <div className="value-box new">
                                    {String(
                                      item.data.new_value
                                    )}
                                  </div>

                                </div>


                              </div>

                            )}


                            <div className="execution">

                              Executed with{" "}

                              <strong>
                                {item.data.execution_method}
                              </strong>

                            </div>


                          </div>

                        )}

                      </>

                    )}


                    {/* AI ERROR */}

                    {item.role === "assistant" &&
                      item.type === "error" && (

                      <>

                        <div className="message-label">
                          AI Excel Automation
                        </div>


                        <div className="error-card">

                          <div className="error-icon">
                            !
                          </div>


                          <div>

                            <strong>
                              Operation failed
                            </strong>

                            <p>
                              {item.text}
                            </p>

                          </div>

                        </div>

                      </>

                    )}


                  </div>

                </div>

              )
            )}


            {/* THINKING */}

            {loading && (

              <div className="message-row assistant">

                <div className="avatar ai-avatar">
                  ✦
                </div>

                <div className="thinking">

                  <span></span>
                  <span></span>
                  <span></span>

                  <label>
                    Working on your Excel file...
                  </label>

                </div>

              </div>

            )}

          </div>

        </section>


        {/* COMPOSER */}

        <div className="composer-wrapper">


          {/* ATTACHED FILE */}

          {file && (

            <div className="file-card">

              <div className="file-icon">
                XLS
              </div>


              <div className="file-info">

                <strong>
                  {file.file_name}
                </strong>

                <span>
                  Connected to local agent
                </span>

              </div>


              <div className="file-check">
                ✓
              </div>

            </div>

          )}


          {/* INPUT */}

          <div className="composer">


            <button
              className="attach-button"
              onClick={selectExcelFile}
              disabled={loading}
              title="Attach Excel file"
            >
              📎
            </button>


            <input
              type="text"
              value={message}
              placeholder={
                file
                  ? "Tell me what you want to change..."
                  : "Attach an Excel file first..."
              }
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={(event) => {

                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {

                  handleSend();

                }

              }}
              disabled={loading}
            />


            <button
              className="send-button"
              onClick={handleSend}
              disabled={
                loading ||
                !message.trim() ||
                !file
              }
            >

              {loading ? "..." : "➤"}

            </button>

          </div>


          <div className="composer-hint">

            AI Excel Automation modifies the original file
            directly on your computer.

          </div>

        </div>

      </main>

    </div>

  );
}

export default App;