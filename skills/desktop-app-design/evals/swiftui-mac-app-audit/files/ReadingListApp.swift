import SwiftUI

struct Article: Identifiable, Hashable {
    let id = UUID()
    var title: String
    var site: String
    var minutes: Int
    var isRead = false
}

@main
struct ReadingListApp: App {
    @AppStorage("darkMode") private var darkMode = false

    var body: some Scene {
        WindowGroup {
            ContentView(darkMode: $darkMode)
                .preferredColorScheme(darkMode ? .dark : .light)
                .frame(width: 900, height: 600)
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
    }
}

struct ContentView: View {
    @Binding var darkMode: Bool
    @State private var articles: [Article] = [
        Article(title: "The Case for Slow Software", site: "example.com", minutes: 12),
        Article(title: "Designing Calm Interfaces", site: "example.org", minutes: 8),
    ]
    @State private var selected: Article?
    @State private var showSettings = false
    @State private var pendingDelete: Article?
    @State private var query = ""

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Button(action: { NSApp.keyWindow?.close() }) {
                    Circle().fill(Color.red).frame(width: 12, height: 12)
                }
                .buttonStyle(.plain)
                Text("📚 Reading List")
                    .font(.system(size: 20, weight: .heavy))
                Spacer()
                Button(action: { showSettings = true }) { Image(systemName: "gearshape") }
                Button(action: share) { Image(systemName: "square.and.arrow.up") }
                    .keyboardShortcut("s", modifiers: .command)
            }
            .padding(14)

            HStack(spacing: 0) {
                ScrollView {
                    VStack(alignment: .leading, spacing: 6) {
                        ForEach(filtered) { article in
                            VStack(alignment: .leading, spacing: 2) {
                                Text(article.title)
                                    .font(.system(size: 14, weight: .semibold))
                                    .foregroundColor(Color(red: 0.15, green: 0.15, blue: 0.15))
                                Text("\(article.site) · \(article.minutes) min")
                                    .font(.system(size: 11))
                                    .foregroundColor(Color(white: 0.65))
                            }
                            .padding(10)
                            .background(selected == article ? Color(red: 0.85, green: 0.9, blue: 1.0) : Color.white)
                            .cornerRadius(10)
                            .onTapGesture {
                                withAnimation(.spring(response: 0.8, dampingFraction: 0.4)) { selected = article }
                            }
                            .contextMenu {
                                Button("Delete") { pendingDelete = article }
                            }
                        }
                    }
                    .padding(12)
                }
                .frame(width: 320)
                .background(Color(red: 0.96, green: 0.96, blue: 0.97))

                Group {
                    if let article = selected {
                        VStack(alignment: .leading, spacing: 12) {
                            Text(article.title).font(.system(size: 26, weight: .bold))
                            Text(article.site).foregroundColor(Color(white: 0.6))
                            Spacer()
                        }
                        .padding(24)
                    } else {
                        Text("No items")
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color.white)
            }

            HStack {
                Image(systemName: "magnifyingglass")
                TextField("Search...", text: $query).textFieldStyle(.plain)
            }
            .padding(10)
            .background(Color(red: 0.93, green: 0.93, blue: 0.94))
        }
        .sheet(isPresented: $showSettings) {
            VStack(spacing: 16) {
                Toggle("Dark mode", isOn: $darkMode)
                HStack {
                    Button("Cancel") { showSettings = false }
                    Button("OK") { showSettings = false }
                }
            }
            .padding(30)
        }
        .alert("Are you sure?", isPresented: Binding(get: { pendingDelete != nil }, set: { if !$0 { pendingDelete = nil } })) {
            Button("Yes", role: .destructive) {
                articles.removeAll { $0.id == pendingDelete?.id }
                pendingDelete = nil
            }
            Button("No", role: .cancel) {}
        }
    }

    private var filtered: [Article] {
        query.isEmpty ? articles : articles.filter { $0.title.localizedCaseInsensitiveContains(query) }
    }

    private func share() {}
}
